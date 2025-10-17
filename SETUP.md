### ⚙️ Setup and Execution Guide

This project requires several components to be configured and run in a specific order.

#### **Prerequisites**
* [IntelliJ IDEA](https://www.jetbrains.com/idea/download/) (with student license)
* [PostgreSQL](https://www.pgadmin.org/download/) with pgAdmin
* [Node.js](https://nodejs.org/en/download)
* ONOS and Mininet installed and configured.

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
