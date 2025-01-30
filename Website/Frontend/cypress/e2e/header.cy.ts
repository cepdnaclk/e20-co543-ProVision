describe("Header", () => {
  // Test 01: Ensure the title is visible
  it('Test 01: Should display the title "TODO APP"', () => {
    cy.visit("/");
    cy.get('[data-testid="cypress-logo"]').contains("TODO APP");
  });

  // Test 02: Ensure the logo is working properly
  it("Test 02: Ensure the logo is working properly", () => {
    // Visit to any directory
    cy.visit("/mytodo");

    // Find the "TODO" text and click it
    cy.get('[data-testid="cypress-logo"]').click();

    // Assert that the URL is now /home
    cy.url().should("include", "/home");
  });

  // Test 03: Should have a pointer cursor when hovering over "TODO" text
  it('Test 03: Should have a pointer cursor when hovering over "TODO" text', () => {
    // Visit any page where the Header is displayed
    cy.visit("/");

    // Verify the cursor style on the "TODO" text
    cy.get('[data-testid="cypress-logo"]').should(
      "have.css",
      "cursor",
      "pointer"
    );
  });

  // Test 04: Should toggle theme on button click
  it("Test 03: Should toggle theme on button click", () => {
    // Visit any page
    cy.visit("/");

    // Find the header background color
    cy.get('[data-testid="cypress-header-background"]').then(($body) => {
      // Get the initial background color
      const initialColor = $body.css("background-color");

      // Click the toggle button
      cy.get('[data-testid="cypress-theme-toggle"]').click();

      // Assert that the background color has changed
      cy.get('[data-testid="cypress-header-background"]').should(($newBody) => {
        const newColor = $newBody.css("background-color");
        expect(newColor).not.to.eq(initialColor); // Ensure it toggled
      });

      // Click the toggle button again to revert
      cy.get('[data-testid="cypress-theme-toggle"]').click();

      // Assert that the background color has reverted
      cy.get('[data-testid="cypress-header-background"]').should(
        ($revertedBody) => {
          const revertedColor = $revertedBody.css("background-color");
          expect(revertedColor).to.eq(initialColor); // Ensure it reverted back
        }
      );
    });
  });
});
