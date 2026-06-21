/** In-memory FIFO queue. ponytail: stands in for a real broker (SQS/Service Bus). */
export class Queue {
  #items = [];

  /** Push a message onto the queue. */
  enqueue(message) {
    this.#items.push(message);
  }

  /** Pop the oldest message, or null if empty. */
  dequeue() {
    return this.#items.length > 0 ? this.#items.shift() : null;
  }

  get size() {
    return this.#items.length;
  }
}
