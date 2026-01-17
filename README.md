# Hands-on DevOps project focused on observability under resource constraints

## 1. Context

This project simulates working on an edge computing robot module with limited resources:

- 2-core CPU (~2 GHz)
- ~500 MB usable RAM
- Docker available

The provided Python sensor service was intentionally inefficient. During testing, it showed:

- CPU spikes
- Increasing memory usage
- Unstable scrape behavior
- Inconsistent response times

My task was to deploy this service, debug and optimize it, and build an observability setup that works reliably under strict memory limits.

---

## 2. Objective

The goal was to build a working observability stack that includes:

- The provided Python sensor service
- A Prometheus-compatible metrics collector
- A visualization layer

**Hard constraint:**  
All components combined must stay below **300 MB RAM** and continue working reliably.

---

## 3. Work Done

### 3.1 Deploying the Sensor Service

I containerized the provided Python service using Docker and ran it as an isolated container.

While running the service and scraping `/metrics`, I observed:

- Frequent metric scrapes
- CPU spikes during request handling
- Growing request counters even without manual traffic

These issues were caused by:

- Inefficient request handling logic
- Uncontrolled metric updates
- Blocking operations during scraping

I simplified the request flow and ensured that:

- Metric updates are lightweight
- Processing latency is consistent
- Scrapes do not trigger heavy CPU work

After optimization, the service became stable under continuous scraping.

---

### 3.2 Metrics System Choice

Instead of running full Prometheus, I chose **VictoriaMetrics (single-node)**.

Reasons for choosing VictoriaMetrics:

- Prometheus-compatible metrics
- Much lower memory usage
- Built-in scraping support
- No separate server + agent needed
- Includes a lightweight UI

This choice reduced:

- Number of containers
- Memory overhead
- Operational complexity

It fits edge environments better than a full Prometheus stack.

---

### 3.3 Visualization Layer

I intentionally did **not** use Grafana.

Grafana adds:

- An extra container
- High baseline memory usage
- Unnecessary overhead for a small edge device

Instead, I used **VictoriaMetrics VMUI**, which:

- Is built-in
- Requires no extra services
- Supports PromQL-compatible queries
- Is sufficient for debugging and analysis

### UI Access

VictoriaMetrics built-in UI can be accessed at:

http://localhost:8428/vmui

This UI was used to:
- Query metrics using PromQL-compatible syntax
- Visualize request counters and latency trends
- Validate system stability under continuous scraping

---

## 4. Performance Budget Report

### Memory Usage (Before vs After)

| Component | Before Optimization (Observed) | After Optimization (Observed) |
|---------|--------------------------------|--------------------------------|
| Sensor Service | ~80–120 MB (unstable, spikes) | ~25–30 MB (stable) |
| Metrics System | Prometheus + Grafana: ~200+ MB | VictoriaMetrics: ~90–100 MB |
| **Total** | **~280–320 MB (often exceeded)** | **~120–130 MB** |

After optimization, the total memory usage stays **well below the 300 MB RAM constraint**, even under continuous scraping.

---

### Notes on “Before” Measurements

- The provided Python sensor service was intentionally inefficient and showed **memory growth and CPU spikes**.
- Memory usage before optimization was inconsistent, so values are reported as **observed ranges**.
- Running Prometheus and Grafana together added a high baseline memory cost.
- During testing, the combined setup **occasionally crossed the 300 MB limit**, causing scrape instability.

---

### Bottlenecks Identified (Before)

- Inefficient request handling logic in the sensor service
- Metric updates coupled directly with request execution
- Blocking operations during `/metrics` scraping
- Heavy observability stack for a constrained edge device

---

### Improvements Applied (After)

- Simplified Python request flow
- Lightweight and controlled metric updates
- Removed blocking logic from the scrape path
- Replaced Prometheus + Grafana with a single VictoriaMetrics instance
- Enforced container-level memory limits

---

### Result

The optimized setup:

- Uses **less than half** of the allowed memory budget
- Remains stable under continuous scraping
- Is suitable for a real-world edge computing environment

---

### Observability Design Decisions

- Minimal number of components
- Predictable memory usage
- Built-in visualization
- Prometheus-compatible metrics

This design prioritizes **stability over features**, which is critical for edge environments.

---

### If Given One More Week

I would:
- Add alerting for sustained CPU spikes
- Simulate higher load patterns
- Add automated stress testing for scrape reliability

---

## 5. How to Run

Start all services using Docker Compose:

    docker-compose up --build

---

## Access Points

### Metrics Endpoint

    http://localhost:8000/metrics

This endpoint exposes Prometheus-compatible metrics from the sensor service.

---

### Visualization UI

    http://localhost:8428/vmui

The VictoriaMetrics VMUI is used to:

- Query metrics using PromQL-compatible syntax  
- Visualize request counters and latency trends  
- Validate stability under continuous scraping  

---

## Final Note

This solution focuses on doing only what is necessary to meet the project goals.

The system is:

- Simple  
- Stable  
- Resource-efficient  
- Well-suited for edge environments with strict memory limits  

All design decisions were made with predictable performance and low operational overhead in mind.


