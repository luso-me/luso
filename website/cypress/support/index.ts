import './commands'

before(() => {
  cy.login();
  cy.saveLocalStorage();
})
