# TODO_APP
A simple full stack todo web app with testing using Typescript. 
This is used to demonstrate the Cypress end-to-end testing framework. 


---

## Cypress Setup for a React Project

### Prerequisites
1. A React project initialized using `create-react-app` or other setups.
2. Node.js and npm/yarn installed on your system.

### Installation
1. Redirect to the working directory.
2. Run the following command to add Cypress
``` powershell
npm install cypress --save-dev
```

### Open Cypress
After installation, open Cypress for the first time to initialize its configuration
``` powershell
npx cypress open
```

This command creates a cypress folder in your project and adds a default `cypress.config.ts` file.

### Update Cypress Config 
Edit cypress.config.ts to customize the base URL for the React app:

```typescript

import { defineConfig } from "cypress";

export default defineConfig({
  e2e: {
    baseUrl: "http://localhost:5173", // Enter base URL here
  },
});
```

### Update `package.json` 
Update the `package.json` file with the following script.
```json
"scripts": {
    "cy:open": "cypress open"
},
```

Make sure to remove the following part from the `package.json` file.
```json
{
  "type": "module"
}
```

### Start Frontend Server
We can use the following CLI to start the frontend server
``` powershell
npm start
```

### Start Backend Server
We can use the following CLI to start the backend server
``` powershell
npm start
```

### Start Cypress
We can use the following CLI to start the Cypress
``` powershell
npm run cy:open
```


---
## Technology Stack 
### * FrontEnd - React + Vite

  ![image](https://github.com/user-attachments/assets/6caa40a9-46a6-46fe-b51c-c4263d96a76d)


### * BackEnd  - Node + Express

  ![image](https://github.com/user-attachments/assets/bdf7c9e8-e941-462c-a321-bc425751b793)


### * Database - MongoDB

  ![image](https://github.com/user-attachments/assets/f9fb4f2b-e9f8-409c-a030-0b18154277af)

### * Testing  - Cypress

  ![image](https://github.com/user-attachments/assets/7b2a572d-903d-436c-bc5d-06861e9ccc71)
