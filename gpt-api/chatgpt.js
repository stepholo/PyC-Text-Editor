const axios = require('axios');
const fs = require('fs');
const path = require('path');

// Function to read the content of a text file
function readFile(filePath) {
    return new Promise((resolve, reject) => {
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                reject(err);
            } else {
                resolve(data);
            }
        });
    });
}

// Main function to interact with the OpenAI API
async function interactWithOpenAI(filePath) {
    try {
        // Read the content of the text file
        const prompt = await readFile(filePath);

        // Request configuration for the OpenAI API
        const config = {
            method: 'post',
            url: 'https://api.openai.com/v1/completions',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer YOUR_API_KEY' // Replace YOUR_API_KEY with your actual API key
            },
            data: {
                model: 'text-davinci-002', // Choose the appropriate model
                prompt: prompt,
                max_tokens: 150 // Adjust as needed
            }
        };

        // Send the request to the OpenAI API
        const response = await axios(config);

        // Print the response from the API
        console.log(response.data.choices[0].text.trim());
    } catch (error) {
        console.error('Error:', error.message);
    }
}

// Extract the file path from command-line arguments
/*const filePath = process.argv[2];

// Check if file path is provided
if (!filePath) {
    console.error('File path not provided.');
    process.exit(1);
}

// Check if the file exists
if (!fs.existsSync(filePath)) {
    console.error('File does not exist.');
    process.exit(1);
}

// Call the main function to interact with the OpenAI API
interactWithOpenAI(filePath);*/
