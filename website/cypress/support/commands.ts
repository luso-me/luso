import "cypress-localstorage-commands";

// https://stackoverflow.com/questions/50820732/in-cypress-set-a-token-in-localstorage-before-test
Cypress.Commands.add("login", () => {
  const jwtAccessToken = Cypress.env('jwtAccessToken');
  const lusoStoreAuth =
      "{\"access_token\": \"" + jwtAccessToken + "\", " +
      "\"token_type\": \"bearer\"}";

  cy.setLocalStorage("luso-store-auth", lusoStoreAuth);

  const userId = Cypress.env("userId");
  const lusoStoreUserInfo =
      "{\"id\":\"" + userId + "\"," +
      "\"gold\":0" + "," + "\"points\":0}";

  cy.setLocalStorage("luso-store-user-info", lusoStoreUserInfo);
});

Cypress.Commands.add("getBySel", (selector, ...args) => {
  cy.get(`[data-test="${selector}"]`, ...args);
});

Cypress.Commands.add("getBySelLike", (selector, ...args) => {
  cy.get(`[data-test*="${selector}"]`, ...args);
});
