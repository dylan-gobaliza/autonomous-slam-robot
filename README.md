# Low-Cost Sonar-Based SLAM Robot

Building an autonomous 2WD indoor mapping platform for the **Arkwright Engineering Scholarship**. 

Instead of using expensive LiDAR or mounting multiple static sensors, this project uses a single **HC-SR04 ultrasonic sonar sensor** mounted on an **SG90 servo motor** executing dynamic 180-degree acoustic sweeps.

---

### The Challenge: High-Risk Indoor Reconnaissance
In urban defense, search-and-rescue, and disaster response, entering unknown or structurally compromised buildings carries extreme human risk. While military-grade Reconnaissance UGVs exist, their high cost (£10,000–£50,000+) makes them too expensive to risk in high-attrition scenarios. Furthermore, heavy smoke, dust, or obscurants can render optical cameras and LiDAR units ineffective due to light scattering.

### The Solution: Expendable Acoustic Mapping (Sonar UGV)
This project develops an **ultra-low-cost (~£37.50) autonomous 2WD recon platform** designed for expendable indoor mapping:
* **Low Cost / High Attrition:** At under £40, if the robot gets damaged or lost in a high-risk area, it’s not a major financial loss compared to a £10k military UGV and it is easily replaceable.
* **Environmental Resilience:** Acoustic ultrasonic pulses penetrate heavy smoke and dark environments that obscure visual LiDAR and camera sensors.

---

## Target Bill of Materials (BOM) & Budget
* Arduino Uno R3 Kit (~£23)
* HC-SR04 Sonar + SG90 Servo (~£4.00)
* HC-05 Bluetooth (~£2.00)
* HC-020K Speed Sensors / Encoders (~£2.00)

* Starter Commercial Chassis -- for testing hardware and identifying flaws when using non-specific templates (~£6.50)

* Chassis: Custom CAD Chassis, laser-cut from recycled school scrap acrylic (£0.00)

* **Total Target Cost: ~£37.50**
* **Equivalent 2D LiDAR Platform (Estimated):** **~£160.00 – £200.00**

---

## 4-Term Roadmap Schedule

* **[x] Term 1 (Y10): Phase 1 — Pygame Simulation Sandbox (Pure Math & 2D Kinematics)**
  * Build 2D software environment to develop understanding of robot kinematics and sonar raycasting math. Also develop simple logic for automation. 
* **[ ] Term 2 (Y10): Phase 2 — 3D Physics & Circuit Simulation (Wokwi & Webots)**
  * Simulate the robot within Webots accounting for sensor noise, physics, etc. Use Wokwi to virtually validate circuit. Identify flaws with commercial chassis and begin development of CAD chassis.
* **[ ] Term 3/4 (Y10/Y11): Phase 3 — Hardware Fabrication & Wireless SLAM**
  * Assembly of harvested motors on laser-cut scrap acrylic, Arduino C++ firmware deployment, and HC-05 Bluetooth SLAM telemetry.

---

## Log / Progress
* **[11/09/26]:** Created repo structure, familiarised myself with Github workflow, and set up development environment. I found it really cool how you can commit straight from VS Code into Github and it saves a lot of time!

* **[12/09/26]:** Created notes.md for raw notes and progression, also started pygame in main.py. Looked briefly over the basic kinematics and math of how the robot works

* **[13/09/26]:** Worked mainly on my iPad, I couldnt understand the math for how to simulate raycasting in python so i worked backwards and managed to prove it! I learnt the formula for the total ray angle and the trig behind raycasting. Honestly it's extremely simple maths it's just the actual concept of what's happening took like 2-3 hours! Also found out apparently this is A-level maths and Year 1 uni level so props to me
