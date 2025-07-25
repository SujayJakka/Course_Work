<!DOCTYPE html>
<html>
<head>
    <title>Sujay Jakka's Term Project Website</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        table { border-collapse: collapse; margin-top: 10px; }
        th, td { border: 1px solid #aaa; padding: 8px; }
        textarea { width: 100%; }
    </style>
</head>
<body>

<h1>Sujay Jakka's Term Project Interface</h1>

<form method="post">
    <label for="sql_query">Enter SQL Query:</label><br>
    <textarea name="sql_query" rows="10"></textarea><br>
    <input type="submit" value="Run Query">
</form>

<?php

require_once __DIR__ . '/../vendor/autoload.php';
$dotenv = Dotenv\Dotenv::createImmutable(__DIR__ . '/../');
$dotenv->load();

// Only runs if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") 
{

    // Gets the SQL query from the form and removes any slashes
    $sql_query = stripslashes($_POST["sql_query"]);

    // Makes sure the SQL query is not a DROP statement
    if (stripos($sql_query, 'DROP') !== false) 
    {
        // Error message if DROP statement is found in the query
        echo "<p style='color: red;'>DROP statements are not allowed.</p>";
        exit;
    }

    // Credential to connect to the database
    $servername = $_ENV["DB_HOST"];
    $username = $_ENV["DB_USER"];
    $password = $_ENV["DB_PASS"];
    $dbname = $_ENV["DB_NAME"];

    // Creates connection to the database
    $conn = new mysqli($servername, $username, $password, $dbname);

    // Checks to see if it is a valid connection
    // If not, it will print an error message
    if ($conn->connect_error) 
    {
        die("<p style='color: red;'>Connection failed: " . $conn->connect_error . "</p>");
    }

    // Find what kind of SQL query it is e.g. INSERT
    $query_type = strtoupper(strtok(trim($sql_query), " "));

    // Checks to see if the SQL query was successful
    if ($result = $conn->query($sql_query)) 
    {
        // If INSERT, UPDATE, DELETE, or CREATE statement was successful,
        // result will return true and one of the following messages will be printed.
        if ($result === true) 
        {
            if ($query_type === "CREATE") 
            {
                echo "<p style='color: green;'>Table Created Successfully.</p>";
            }
            elseif ($query_type === "UPDATE") 
            {
                echo "<p style='color: green;'>Table Updated Successfully.</p>";
            } 
            elseif ($query_type === "INSERT") 
            {
                echo "<p style='color: green;'>Row(s) Inserted Successfully.</p>";
            } 
            elseif ($query_type === "DELETE") 
            {
                echo "<p style='color: green;'>Row(s) Deleted Successfully.</p>";
            } 
            else 
            {
                echo "<p style='color: green;'>SQL Query was executed successfully.</p>";
            }
        }
        // SELECT statement will return rows if successful
        // Will print the results as a table
        elseif ($result->num_rows > 0) 
        {
            echo "<p><strong>Query Results:</strong></p>";
            echo "<table><tr>";

            // Prints column headers
            while ($field = $result->fetch_field()) {
                echo "<th>" . $field->name . "</th>";
            }
            echo "</tr>";

            // Prints rows
            while ($row = $result->fetch_assoc()) {
                echo "<tr>";
                // Loops through each cell in the row and prints it
                foreach ($row as $cell) {
                    echo "<td>" . $cell . "</td>";
                }
                echo "</tr>";
            }
            echo "</table>";

            // Print number of rows returned
            echo "<p style='color: green;'>Number of rows returned: " . $result->num_rows . "</p>";
        }
        // If the SELECT statement was successful but no rows were returned
        // Will print the following message
        else 
        {
            echo "<p>No results found. 0 rows returned.</p>";
        }
    }
    // If the SQL query was not successful, it will print an error message from the database
    else 
    {
        echo "<p style='color: red;'>Error: " . $conn->error . "</p>";
    }

    // Closes the connection to the database
    $conn->close();
}
?>

</body>
</html>