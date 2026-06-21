/** Notification worker: drains a queue and "sends" each message, with retry. */
import { Queue } from "./queue.js";

const MAX_ATTEMPTS = 3;
const POLL_INTERVAL_MS = 1000;

/** Pretend to deliver a notification. Throws to simulate transient failures. */
async function deliver(message) {
  if (!message.to || !message.body) {
    throw new Error("message missing 'to' or 'body'");
  }
  // ponytail: real impl would call an email/SMS provider here.
  console.log(`[notifier] delivered to ${message.to}: ${message.body}`);
}

/** Process one message with bounded retries. Returns true if delivered. */
export async function processMessage(message) {
  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
    try {
      await deliver(message);
      return true;
    } catch (err) {
      console.warn(`[notifier] attempt ${attempt} failed: ${err.message}`);
      if (attempt === MAX_ATTEMPTS) return false;
    }
  }
  return false;
}

/** Poll the queue forever, processing messages as they arrive. */
export async function run(queue) {
  for (;;) {
    const message = queue.dequeue();
    if (message === null) {
      await new Promise((resolve) => setTimeout(resolve, POLL_INTERVAL_MS));
      continue;
    }
    await processMessage(message);
  }
}

// Start only when run directly, not when imported by tests.
// Welcome events are produced by the backend (see backend/app/events.py).
if (import.meta.url === `file://${process.argv[1]}`) {
  const queue = new Queue();
  queue.enqueue({ recipient: "admin@example.com", message: "Welcome aboard" });
  run(queue);
}
