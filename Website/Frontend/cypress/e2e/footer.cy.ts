describe("Footer", () => {
  // Test 01: Should display the copyright information
  it("Test01: Should display the copyright information", () => {
    cy.visit("/");
    cy.get('[data-testid="cypress-footer"]').should(
      "have.text",
      "All rights reserved © 2025 PeraBytes"
    );
  });

  // Test 02: Checking CSS
  it("Test 02: Should have correct styles", () => {
    cy.visit("/");
    cy.get('[data-testid="cypress-footer"]').should(
      "have.css",
      "text-align",
      "center"
    );
  });
});
