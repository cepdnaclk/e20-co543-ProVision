// Home Page Testing
describe("Home Page", () => {
  // Test 01: Should load the Home Page properly
  it("Test 01: should load the Home Page properly", () => {
    // Visit
    cy.visit("/home");

    // Check the logo
    cy.get('[data-testid="cypress-pbLogo"]').should("be.visible");

    // Check Welcome Note
    cy.get('[data-testid="cypress-welcomeMsg"]').should(
      "have.text",
      "Welcome Back"
    );

    // Check the todo button
    cy.get('[data-testid="cypress-todoButton"]')
      .should("be.visible")
      .should("have.text", "VIEW MY TODO");
  });

  // Test 02: Should navigate to Todo page when "View My TODO" button is clicked
  it('Test 02: Should navigate to Todo page when "View My TODO" button is clicked', () => {
    // Visit Home Page
    cy.visit("/");

    // Find the button
    cy.get('[data-testid="cypress-todoButton"]').click();

    // Ensure navigation to the Todo page
    cy.url().should("include", "/mytodo");
  });
});
