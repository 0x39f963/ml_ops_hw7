import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 10,
  duration: "30s",
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<500"],
    checks: ["rate>0.99"],
  },
};

export default function () {
  const health = http.get("http://127.0.0.1:18080/health", {
    headers: { Accept: "application/json" },
  });
  check(health, {
    "health status is 200": (r) => r.status === 200,
    "health status ok": (r) => r.json("status") === "ok",
  });

  const predict = http.post(
    "http://127.0.0.1:18080/predict",
    JSON.stringify({ x: [1, 2, 3] }),
    { headers: { "Content-Type": "application/json" } },
  );
  check(predict, {
    "predict status is 200": (r) => r.status === 200,
    "predict has version": (r) => Boolean(r.json("version")),
  });

  sleep(1);
}
