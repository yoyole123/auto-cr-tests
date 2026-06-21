import assert from "node:assert/strict";
import { test } from "node:test";

import { Queue } from "./queue.js";
import { processMessage } from "./index.js";

test("queue is FIFO", () => {
  const q = new Queue();
  q.enqueue("a");
  q.enqueue("b");
  assert.equal(q.dequeue(), "a");
  assert.equal(q.dequeue(), "b");
  assert.equal(q.dequeue(), null);
});

test("processMessage delivers a valid message", async () => {
  assert.equal(await processMessage({ to: "x@y.com", body: "hi" }), true);
});

test("processMessage gives up on a permanently invalid message", async () => {
  assert.equal(await processMessage({ to: "", body: "" }), false);
});
