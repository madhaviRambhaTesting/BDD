Feature: Login Functionality

  Scenario: Successful login
    Given I am on the login page
    When I enter a valid username
    And I enter a valid password
    And I click the login button
    Then I should see the "Products" page
    And there should be only one window open