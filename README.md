Install Backend Dependencies

bash

pip install -r requirements.txt

3. Install Frontend Dependencies

Make sure you navigate to the frontend directory if applicable:

bash

npm install

4. Environment Variables

Create a .env file in the root directory and add the following environment variables:

bash

ACCOUNT_ADDRESS=your_eth_account_address
PRIVATE_KEY=your_private_key

5. Smart Contract Compilation

Ensure you have the compiled contract (JSON ABI and bytecode) in the build directory. If not, compile the Solidity contract using tools like Remix or Truffle, and save the ABI and bytecode in AcademicCredentials.json.
6. Run Ganache

Open Ganache and start a local blockchain at http://127.0.0.1:7545.
7. Run the Backend

bash

python app.py

8. Run the Frontend

bash

npm run dev

The frontend will now be running at http://localhost:3000.
