#!/usr/bin/node

const fs = require('fs');
const axios = require('axios');
const { interactWithOpenAI } = require('../../gpt-api/chatgpt.js');

jest.mock('fs');
jest.mock('axios');

describe('interactWithOpenAI', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should call OpenAI API and append response to file', async () => {
    const fileContent = 'Test file content';
    const filePath = 'C:\\Users\\LENOVO\\Desktop\\PyC-Text-Editor-1\\test\\file.txt';
    const response = { data: { choices: [{ text: 'Test AI response' }] } };

    axios.mockResolvedValue(response);
    fs.appendFileSync.mockImplementation((path, data) => {});

    await interactWithOpenAI(fileContent, filePath);
    console.log(axios.mock.calls);
    expect(axios).toHaveBeenCalledWith({
      method: 'post',
      url: 'https://api.openai.com/v1/completions',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer'
      },
      data: {
        model: 'text-davinci-002',
        prompt: 'Test file content',
        max_tokens: 150
      }
    });

    expect(fs.appendFileSync).toHaveBeenCalledWith(
      filePath,
      "\n\nChatGPT Response:\nTest AI response\n"
    );
  });

  it('should handle errors', async () => {
    const fileContent = 'Test file content';
    const filePath = 'C:\\Users\\LENOVO\\Desktop\\PyC-Text-Editor-1\\test\\file.txt';
    const errorMessage = 'Request failed with status code 401';

    axios.mockRejectedValue(new Error(errorMessage));
    fs.appendFileSync.mockImplementation((path, data) => {});

    await interactWithOpenAI(fileContent, filePath);

    expect(fs.appendFileSync).toHaveBeenCalledWith(
      filePath,
      "\n\nChatGPT Response:\n" + errorMessage
    );
  });
});
