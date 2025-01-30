// API Testing

const END_POINT_URL = "http://localhost:5000/api/todos";

describe("API Testing", () => {
  // Test 01: Should fetch todos from the API
  it("Test 01: Should fetch todos from the API", () => {
    cy.request("GET", END_POINT_URL).its("status").should("eq", 200); // Check if the response is successful
  });

  // Test 02: Should add a new todo via API
  it("Test 02: Should add a new todo via API", () => {
    cy.request("POST", END_POINT_URL, {
      title: "Test Todo",
      content: "Content for test todo",
      dueDate: "2025-01-15",
    })
      .its("status")
      .should("eq", 201); // Ensure the response is successful
  });

  // Test 03: Should delete a todo via API
  it("Test 03: Should delete a todo via API", () => {
    cy.request("DELETE", END_POINT_URL, { id: "1" })
      .its("status")
      .should("eq", 200); // Ensure the response is successful
  });
});
