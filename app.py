"""Flask Queue Simulator (FIFO): Enqueue, Dequeue, Peek, Clear."""
import secrets

from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash)
from queue_model import Queue

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

MAX_ITEMS = 20
MAX_LENGTH = 24


@app.route('/')
def index():
    queue = Queue(session.get('queue', []))
    removed = session.get('removed', [])
    highlight = session.pop('peek', False)  # highlight lasts for one page load
    return render_template(
        'index.html',
        items=queue.items,          # front first, rear last
        size=queue.size(),
        removed=removed,
        highlight=highlight,
    )


@app.route('/queue', methods=['POST'])
def operate():
    action = request.form.get('action', '')
    value = request.form.get('value', '').strip()

    queue = Queue(session.get('queue', []))
    removed = list(session.get('removed', []))

    if action == 'enqueue':
        if not value:
            flash('Please enter a value before enqueueing.', 'error')
        elif len(value) > MAX_LENGTH:
            flash(f'Value is too long (max {MAX_LENGTH} characters).', 'error')
        elif queue.size() >= MAX_ITEMS:
            flash(f'Queue is full (max {MAX_ITEMS} items).', 'error')
        else:
            queue.enqueue(value)
            flash(f'Enqueued {value} at the rear.', 'success')

    elif action == 'dequeue':
        if queue.is_empty():
            flash('Cannot dequeue: the queue is empty.', 'error')
        else:
            front = queue.dequeue()
            removed.append(front)
            removed = removed[-MAX_ITEMS:]
            flash(f'Dequeued {front} from the front.', 'success')

    elif action == 'peek':
        if queue.is_empty():
            flash('Cannot peek: the queue is empty.', 'error')
        else:
            session['peek'] = True
            flash(f'Front value is {queue.peek()} (not removed).', 'success')

    elif action == 'clear':
        queue.clear()
        removed = []
        flash('Queue and removed items cleared.', 'success')

    else:
        flash('Unknown action.', 'error')

    session['queue'] = queue.items
    session['removed'] = removed
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
