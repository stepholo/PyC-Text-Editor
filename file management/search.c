#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to find a string in the text
int find(const char *search_text, const char *file_content) {
    const char *result = strstr(file_content, search_text);
    if (result != NULL) {
        printf("'%s' found at position %lld\n", search_text, result - file_content);
        return 1; // Success
    } else {
        printf("'%s' not found\n", search_text);
        return 0; // Failure
    }
}
/*
int loader() {
    // Open the text file
    FILE *file = fopen("me.txt", "r");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }

    // Get the size of the file
    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    fseek(file, 0, SEEK_SET);

    // Allocate memory to store the file contents
    char *text = malloc(file_size + 1);
    if (text == NULL) {
        perror("Error allocating memory");
        fclose(file);
        return 1;
    }

    // Read the file contents into the text variable
    if (fread(text, 1, (size_t)file_size, file) != (size_t)file_size) {
        perror("Error reading file");
        fclose(file);
        free(text);
        return 1;
    }

    // Null-terminate the string
    text[file_size] = '\0';

    // Close the file
    fclose(file);

    // Test the find function
    find("is", text); // Replace "search_text" with your desired search text

    // Free allocated memory
    free(text);

    return 0;
}*/