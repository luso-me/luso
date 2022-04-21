import "cypress-localstorage-commands";

describe("Home Index Page", () => {

  beforeEach(() => {
    cy.restoreLocalStorage();
  });

  it("should display logout button", () => {
    cy.visit("/");
    cy.getBySel("home-index-logout").should('contain', 'Logout');
  });

  it("should display github login button", () => {
    cy.clearLocalStorage();
    cy.visit("/");
    cy.getBySel("home-index-github-login").should('contain', 'Login');
    cy.login();
    cy.saveLocalStorage();
  });

  /*todo: https://gist.github.com/jhaynie/1db3a38acdc7977fc66c483d4516d613*/
  it("todo : login to github", () => {
    console.log("todo");
  });
});



