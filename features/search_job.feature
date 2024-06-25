
Feature: Search job

  Scenario: User can log in on Linkedin with valid credentials and search a job
    Given the user is on the login page
    When the user logs in with valid credentials
    Then the user should be redirected to the dashboard
    When the user go to the LinkedIn jobs search page
    And the user searches for a job title "QA" in "América Latina"
    And the user opens the filter panel
    And the user selects the filter "Ultimas 24 horas"
    And the user selects the filter "Remoto"
    #And the user selects the filter "Hibrido"
    #And the user selects the filter "Presencial"
    #And the user selects the filter "Semana pasada"
    #And the user selects the filter "Mes pasado"
    #And the user selects the filter "Cualquier momento"
    #And the user selects the filter "Mas recientes"
    #And the user selects the filter "Mas relevantes"
    #And the user selects single application filter
    Then the search results should be displayed
    And the user navigates through all the results
    And the user logout
