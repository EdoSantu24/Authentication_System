# SDN-based Host Authentication Service

**Project by:** Edoardo Santucci & Gea Staropoli

This repository contains the source code for a university project that implements a dynamic, topology-independent authentication service for a Software-Defined Network (SDN). The system uses the ONOS controller to enforce a "default-deny" security policy, where all hosts are initially blocked from communicating. Access is granted only after a host successfully authenticates through a web-based login portal.

This project was developed for the "Software-Defined Networking" (34359) course at the Technical University of Denmark (DTU).

---

### Key Features

* **Zero-Trust Network Policy:** All host-to-host communication is blocked by default until explicit authentication.
* **Dynamic Flow Rule Management:** The system interacts with the ONOS REST API to dynamically install and remove flow rules on network switches.
* **Topology-Agnostic Design:** The service automatically discovers the network topology (hosts, switches, links) and applies rules accordingly, making it adaptable to any network structure.
* **Web-Based Authentication Portal:** Hosts authenticate using a user-friendly web interface.
* **Decoupled Multi-Component Architecture:** The solution integrates several technologies, including a Java-based firewall, a web application with a Java Servlet backend, a Node.js server for credential verification, and a PostgreSQL database.

---

### Technology Stack

* **SDN Controller:** ONOS (Open Network Operating System)
* **Network Emulation:** Mininet
* **Backend Services:** Java, Java Servlets, Node.js (Express.js)
* **Web Server:** GlassFish
* **Database:** PostgreSQL
* **Development Environment:** IntelliJ IDEA
* **Topology Scripting:** Python

#### **Prerequisites**
* [IntelliJ IDEA](https://www.jetbrains.com/idea/download/)
* [PostgreSQL](https://www.pgadmin.org/download/) with pgAdmin
* [Node.js](https://nodejs.org/en/download)
* ONOS and Mininet installed and configured.

---

### System Workflow

The service is composed of several interconnected components that work together to manage network access. The core interaction is between the custom applications and the ONOS SDN controller.

1.  **ONOS & Mininet:** The **ONOS Controller** acts as the "brain" of the network. A custom network topology is created using **Mininet** and a Python script, which ONOS then discovers and manages.
2.  **Firewall Service (Java Application):** On startup, this application queries the ONOS REST API to get the full network topology. It then iterates through all host pairs and installs **`DROP` flow rules** on the relevant switches, blocking all traffic.
3.  **Authentication Web Application (Java Servlet + JSP):**
    * A user on a host attempts to access the network and is directed to a **login page** (JSP served by a GlassFish server).
    * The user submits their credentials.
4.  **Credential Verification (Node.js + PostgreSQL):**
    * The login page sends the credentials to a lightweight **Node.js server**.
    * The Node.js server queries a **PostgreSQL database** to validate the username and password.
5.  **Granting Access:**
    * If credentials are valid, the Node.js server informs the web application.
    * The web application's Java Servlet (`pushRule`) is triggered. It identifies which switch the authenticated host is connected to (via the ONOS API) and sends commands to **`REMOVE` the specific `DROP` rules** associated with that host.
6.  **Authenticated Communication:** The host is now able to communicate with other authenticated hosts on the network.


---

### ⚙️ Setup and Execution Guide

This project requires several components to be configured and run in a specific order.

#### **1. Repository Setup**
Clone this repository and extract the project zip files (`Firewall_final.zip`, `SDNAuth_final.zip`) and the topology script (`Topology.py`).

#### **2. Database Configuration**
1.  Using **pgAdmin**, create a new database named `sdn_proj`.
2.  Open the Query Tool for the `sdn_proj` database.
3.  Execute the following SQL commands to create the `users` table and populate it with initial host credentials:
    ```sql
    CREATE TABLE users (
        us VARCHAR(256) PRIMARY KEY,
        psw VARCHAR(256),
        conn BOOLEAN
    );

    INSERT INTO users (us, psw, conn) VALUES
        ('h1', 'h1', false),
        ('h2', 'h2', false),
        ('h3', 'h3', false),
        ('h4', 'h4', false);
    ```

#### **3. Application Configuration**
1.  **Authentication App (`SDNAuth_final`):**
    * Open the project in IntelliJ.
    * Configure a **GlassFish 4.1.1** application server.
    * In the integrated terminal, navigate to the project directory and install the Node.js dependencies:
        ```bash
        npm install express pg cors
        ```
2.  **Firewall App (`Firewall_final`):**
    * Open the project in IntelliJ.

#### **4. Execution Flow**
The system must be launched in the following order:

1.  **Start ONOS:**
    * In a new terminal, run `bazel run onos-local -- clean`.
    * Once complete, in a second terminal, run `onos localhost` to access the ONOS CLI.
2.  **Launch Network Topology:**
    * In a third terminal, navigate to the location of `Topology.py` and run: `sudo python Topology.py`. This will start Mininet.
    * At this point, you can test that all hosts can ping each other (`pingall` in the Mininet CLI).
3.  **Run the Firewall Service:**
    * In IntelliJ, run the `Firewall_final` application.
    * After it completes, test connectivity in Mininet again (`pingall`). All pings should now fail (100% packet drop).
4.  **Run the Authentication Service:**
    * In IntelliJ, within the `SDNAuth_final` project, first run the `Lancia.js` Node.js server.
    * Once the server confirms it's running, run the main `SDNAuth_final` application.
5.  **Authenticate Hosts:**
    * A login page will open in your browser.
    * Log in as `h1` (password: `h1`). After the "Login successful" pop-up, `h1` is authenticated.
    * Log in as `h2` (password: `h2`).
    * Now, go to the Mininet CLI and test connectivity between `h1` and `h2` (`h1 ping h2`). The ping should now succeed.

---

### 📄 Documentation

The full project report, containing in-depth details about the design, implementation, and testing, can be found here: **[Project Report](./docs/SDN.pdf)**
