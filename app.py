"""Flask Stack Simulator (LIFO): Push, Pop, Peek, Clear."""
import secrets

from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash)
from stack_model import Stack

app = Flask(__name__)
# Needed for session and flash messages (fictional values, localhost only).
app.config['SECRET_KEY'] = secrets.token_hex(16)

MAX_ITEMS = 20
MAX_LENGTH = 24


@app.route('/')
def index():
    stack = Stack(session.get('stack', []))
    popped = session.get('popped', [])
    highlight = session.pop('peek', False)  # highlight lasts for one page load
    return render_template(
        'index.html',
        items=list(reversed(stack.items)),  # top of the stack is shown first
        size=stack.size(),
        popped=popped,
        highlight=highlight,
    )


@app.route('/stack', methods=['POST'])
def operate():
    action = request.form.get('action', '')
    value = request.form.get('value', '').strip()

    stack = Stack(session.get('stack', []))
    popped = list(session.get('popped', []))

    if action == 'push':
        if not value:
            flash('Please enter a value before pushing.', 'error')
        elif len(value) > MAX_LENGTH:
            flash(f'Value is too long (max {MAX_LENGTH} characters).', 'error')
        elif stack.size() >= MAX_ITEMS:
            flash(f'Stack is full (max {MAX_ITEMS} items).', 'error')
        else:
            stack.push(value)
            flash(f'Pushed {value} onto the stack.', 'success')

    elif action == 'pop':
        if stack.is_empty():
            flash('Cannot pop: the stack is empty.', 'error')
        else:
            removed = stack.pop()
            popped.append(removed)
            popped = popped[-MAX_ITEMS:]  # keep 20 most recent removed values
            flash(f'Popped {removed} from the top.', 'success')

    elif action == 'peek':
        if stack.is_empty():
            flash('Cannot peek: the stack is empty.', 'error')
        else:
            session['peek'] = True
            flash(f'Top value is {stack.peek()} (not removed).', 'success')

    elif action == 'clear':
        stack.clear()
        popped = []
        flash('Stack and removed items cleared.', 'success')

    else:
        flash('Unknown action.', 'error')

    session['stack'] = stack.items
    session['popped'] = popped
    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)  # Local development only. Stop with Ctrl+C.
