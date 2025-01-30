// Todo Page Testing
describe("Todo Page", () => {
  // Test 01 : should load the MyTodo page properly
  it("Test 01 : should load the MyTodo page properly", () => {
    // Visit the MyTodo page
    cy.visit("/mytodo");

    // Verify the URL is correct
    cy.url().should("include", "/mytodo");

    // Check if the Create New Todo section is present properly
    cy.get('[data-testid="cypress-NewTodoSection"]').should("be.visible");
    cy.get('[data-testid="cypress-NewTitle"]').should("be.visible");
    cy.get('[data-testid="cypress-NewDate"]').should("be.visible");
    cy.get('[data-testid="cypress-NewContent"]').should("be.visible");
    cy.get('[data-testid="cypress-CancelBtn"]').should("be.visible");
    cy.get('[data-testid="cypress-AddBtn"]').should("be.visible");

    // Check if the Todo List section is present
    cy.get('[data-testid="cypress-TodoListSection"]')
      .should("be.visible")
      .should("have.text", "My Todo List");
  });

  // Test 02: Should display the list of todos
  it("Test 02: Should display the list of todos", () => {
    // Visit the /mytodo page
    cy.visit("/mytodo");

    // Ensure the todo list section exists
    cy.get('[data-testid="cypress-TodoListSection"]').should("exist");

    // Wait for the todo cards to be rendered
    cy.get('[data-testid="cypress-TodoCard"]').should(
      "have.length.greaterThan",
      0
    );

    // Validate the structure of a TodoCard
    cy.get('[data-testid="cypress-TodoCard"]').each(($todo) => {
      cy.wrap($todo).within(() => {
        // Title
        cy.get('[data-testid="CardTitle"]').should("exist").and("not.be.empty");

        // Due Date
        cy.get('[data-testid="CardDue"]').should("exist").and("not.be.empty");

        // Content
        cy.get('[data-testid="CardContent"]')
          .should("exist")
          .and("not.be.empty");

        // Delete Button
        cy.get('[data-testid="CardButton"]')
          .should("exist")
          .and("have.text", "Mark as Done");
      });
    });
  });

  // Test 03: Should allow adding a new todo
  it("Test 03: Should allow adding a new todo", () => {
    // Intercept the POST request made by the addEvent function
    cy.intercept("POST", "**/api/todos").as("addTodo");

    // Visit
    cy.visit("/mytodo");

    // Filling input fields with new data
    cy.get('[data-testid="cypress-NewTitle"]').type("New Test Todo");
    cy.get('[data-testid="cypress-NewDate"]').type("2025-01-16");
    cy.get('[data-testid="cypress-NewContent"]').type("This is a new todo.");

    // Find and click Add New content
    cy.get('[data-testid="cypress-AddBtn"]').click();

    // Verify the system added the item successfully to the todo list
    cy.wait("@addTodo").its("response.statusCode").should("eq", 201);
  });

  // Test 04: Should delete a todo
  it("Test 04: Should delete a todo", () => {
    // Intercept the DELETE request made by the removeEvent function
    cy.intercept("DELETE", "**/api/todos").as("removeTodo");

    // Visit
    cy.visit("/mytodo");

    // Get the first todo and mark it as done
    cy.get('[data-testid="cypress-TodoCard"]')
      .first()
      .find("button")
      .contains("Mark as Done")
      .click();

    // Verify the system removed the item successfully from the todo list
    cy.wait("@removeTodo").its("response.statusCode").should("eq", 200);
  });
});
