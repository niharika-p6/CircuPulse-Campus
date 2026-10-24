# SRUJANA 2026: Official 2-Minute 30-Second Product Demonstration Script
**Product Name:** CircuPulse Campus (Predictive Circular-Resource Grid)  
**Target Video Duration:** Exactly 2 minutes and 30 seconds (150 seconds max)  
**Presenter Guidelines:** Speak clearly with steady pacing (~130 words per minute). Record screen in full 1080p resolution with the Streamlit app running locally (`streamlit run app.py`).

---

## Visual Cue & Spoken Script Breakdown

```mermaid
timeline
    title 2:30 Demo Video Narrative Arc
    0:00 - 0:25 : Problem & Campus Overview
    0:25 - 0:55 : 12-Hour Predictive Forecaster
    0:55 - 1:25 : Real-Time Edge Smart-Bin Classifier
    1:25 - 1:55 : Offline Gateway Buffer & Reconciliation
    1:55 - 2:25 : Forensic Root-Cause & CircuCredits
    2:25 - 2:30 : Scalability & Conclusion
```

---

### [0:00 – 0:25] ACT 1: The Problem & Campus Circular Overview
* **Screen Display:** Open Streamlit dashboard on **"🌐 Executive Campus Grid"**.
* **Action on Screen:** Move cursor over the top 4 KPI cards (750k kWh Grid, 109k kWh Solar Offset, 72.2% Diversion, ₹875k Saved). Select **"B07: Food Court"** in the Building Directory and highlight the Circular Flow breakdown.
* **Spoken Script (Voiceover):**  
  > *"Every day, multi-building university campuses waste millions in utility spikes, generate unsegregated landfill waste, and struggle with delayed facility audits.  
  > Welcome to **CircuPulse Campus**, an AI-driven predictive circular-resource grid built for SRUJANA 2026.  
  > Connected to 8 campus facilities across 120 operational days, CircuPulse fuses heterogeneous energy, water, and waste streams. By tracking decentralized flows—like 30,000 kg of Food Court wet waste converted into 17,000 kg of botanical compost—we achieve a verified 72.2% circular diversion rate and over 76,000 kg of avoided carbon."*

---

### [0:25 – 0:55] ACT 2: Short-Horizon Predictive Demand Forecaster
* **Screen Display:** Click **"🔮 12-Hour Predictive Forecaster"** in the sidebar.
* **Action on Screen:** Select **"B01: Academic Block A"** and utility **"electricity_kwh"**. Hover over the orange dashed forecast line showing the $95\%$ confidence ribbon and point out the **77.1% error reduction** metric card.
* **Spoken Script (Voiceover):**  
  > *"Facilities teams cannot afford to react after peak meal hours or exam rushes occur.  
  > CircuPulse features a short-horizon autoregressive time-series engine running closed-form Ridge Regression. By combining 24-hour diurnal rhythms, weekly seasonality, and academic schedule context, our model predicts building-level surges 6 to 12 hours ahead.  
  > On holdout competition data, our forecaster achieves a Mean Absolute Error of just 6.05 kWh—slashing prediction error by 77.1% compared to traditional persistence baselines, giving facility managers time to pre-cool lecture halls and optimize solar storage."*

---

### [0:55 – 1:25] ACT 3: Real-Time Edge Smart-Bin Sorter
* **Screen Display:** Click **"🗑️ Edge Smart-Bin Sorter"** in the sidebar.
* **Action on Screen:** In the Point-of-Disposal Simulator, click the preset **"Aluminium Beverage Can"** (sliders move: metal 85, weight 95g). Show the instant green card: **"Categorized as: METAL (99.8% confidence, 1.4 ms latency)"**. Then switch preset to **"Food Peel / Organic Waste"** and show the instant probability redistribution.
* **Spoken Script (Voiceover):**  
  > *"Contamination in recycling bins ruins circularity. At the point of disposal, we deploy our multi-modal edge classifier.  
  > Running Gaussian Naive Bayes directly on low-cost microcontrollers with zero cloud dependencies, the system fuses five physical sensor signals: load cell weight, dielectric moisture, inductive metal proximity, optical transparency, and acoustic impact resonance.  
  > It achieves 85.11% accuracy across 6 waste categories with an edge inference latency of just 1.4 milliseconds—more than 1,000 times faster than the competition's 2-second edge requirement. We’ve already batch-classified all 1,601 unlabelled active test stream events."*

---

### [1:25 – 1:55] ACT 4: Intermittent Gateway Buffer & Lossless Recovery
* **Screen Display:** Click **"📡 Gateway Buffer & Recovery"** in the sidebar.
* **Action on Screen:** Point out the **"368 Redundant Retransmissions Pruned"** metric card. Move the blackout slider to **6 Hours** for Boys Hostel (B05), then click the blue button: **"🔄 Trigger Reconnection & Burst Flush"**.
* **Spoken Script (Voiceover):**  
  > *"In real campus deployments, buildings frequently lose network connectivity. CircuPulse is engineered for harsh IoT conditions.  
  > When a building gateway disconnects, readings queue in local flash memory. Upon reconnection, telemetry flushes in a burst batch.  
  > Our cloud ingestion engine automatically sorts out-of-order packets and deterministically deduplicates retransmitted network retries—pruning 184 redundant duplicates from the benchmark stream with 100% lossless data integrity, ensuring campus dashboards never display corrupted trends."*

---

### [1:55 – 2:25] ACT 5: Explainable Incident Forensics & Behavioral Incentives
* **Screen Display:** Click **"🔍 Forensics & CircuCredits"**.
* **Action on Screen:** Expand the first card **"[INC-01] Water Utility Anomaly — Girls Hostel"**. Point out the corroborating log: *"Plumber called; underground pipe leak repaired"*, then click the **"🏆 CircuCredit Dorm Leaderboard"** tab to show the ranked table.
* **Spoken Script (Voiceover):**  
  > *"CircuPulse goes beyond raw dashboards to explain root causes. Our forensic engine autonomously pairs statistical telemetry surges with human field logs. For example, in August at Girls Hostel, it detected an 8,000-liter water surge, corroborated it with the warden's note on an underground pipe leak, and quantified ₹2,400 in preventable losses.  
  > To close the loop, our 'CircuCredit' gamification engine normalizes resource consumption by active occupant-days. Hostels with 600 students compete fairly on a per-capita basis against academic halls, earning tier badges and driving measurable behavioral reduction."*

---

### [2:25 – 2:30] CONCLUSION & CALL TO ACTION
* **Screen Display:** Switch to **"⚙️ Architecture & Hardware Budget"**, showing the **$280/building BOM** and scaling envelope.
* **Spoken Script (Voiceover):**  
  > *"At just $280 per building and architected to scale effortlessly from 8 to 30+ buildings, CircuPulse Campus transforms raw telemetry into a circular, resilient, and intelligent university grid. Thank you!"*

---

## Recording Checklist for the Team

- [ ] Resolution set to 1920x1080 (16:9).
- [ ] Microphone tested with clear audio levels and zero background noise.
- [ ] Streamlit sidebar open and smoothly navigated through the 6 views.
- [ ] Practice run timed: Aim for **2 minutes 15 seconds to 2 minutes 25 seconds** to stay comfortably within the 2:30 maximum limit.
- [ ] Save output as standard MP4 for final submission portal upload.
