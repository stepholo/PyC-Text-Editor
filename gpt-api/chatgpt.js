// Import required modules
const axios = require('axios');
const fs = require('fs');

// Main function to interact with the OpenAI API
async function interactWithOpenAI(fileContent, filePath) {
    console.log("Received input data:");
    console.log("File Content:", fileContent);
    console.log("File Path:", filePath);
    try {

        // Request configuration for the OpenAI API
        const config = {
            method: 'post',
            url: 'https://api.openai.com/v1/completions',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer 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'
            },
            data: {
                model: 'text-davinci-002', // Choose the appropriate model
                prompt: fileContent,
                max_tokens: 150 // Adjust as needed
            }
        };

        // Send the request to the OpenAI API
        const response = await axios(config);

        // Append the response to the same file
        fs.appendFileSync(filePath, "\n\nChatGPT Response:\n" + response.data.choices[0].text.trim() + "\n");
    } catch (error) {
        console.error('Error:', error.message);
    }
}

// Export the function to make it accessible from Python
module.exports = {
    interactWithOpenAI
};

// Check if this script is executed from command line
if (require.main === module) {
    // Extracting command line arguments
    const [, , fileContent, filePath] = process.argv;

    // Call the main function with provided arguments
    interactWithOpenAI(fileContent, filePath);
}