#!/usr/bin/env node

// Import required modules
const fs = require('fs');
const { OpenAI } = require('openai');

const openai = new OpenAI({ apiKey: '' });

// Main function to interact with the OpenAI API
async function interactWithOpenAI(fileContent, filePath) {
    try {

        // Request configuration for the OpenAI API
        const completion = await openai.chat.completions.create({
            messages: [{ role: "system", content: fileContent }],
            model: "gpt-3.5-turbo"
        })

        // Append the response to the same file
        fs.appendFileSync(filePath, "\nChatGPT Response:\n" + completion.choices[0].message.content + "\n\nUser Response\n");
    } catch (error) {
        // Append the error as well
        fs.appendFileSync(filePath, "\n\nChatGPT Response:\n" + error.message)

    }
}

// Check if this script is executed from command line
if (require.main === module){
    // Extracting command line arguments
    const [, , fileContent, filePath] = process.argv;

    // Call the main function with provided arguments
    interactWithOpenAI(fileContent, filePath);
}