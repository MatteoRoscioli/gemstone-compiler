let functions = {};

function processInstruction(instruction) {
  const parts = instruction.split();

  if (parts[0].toUpperCase() === "EXIT") {
    return false; // Signal to stop
  }

  if (parts[0].toUpperCase() === "ADD") {
    const num1 = parseInt(parts[1]);
    const num2 = parseInt(parts[2]);
    const result = num1 + num2;
    console.log(`Result: ${result}`);
  } else if (parts[0].toUpperCase() === "PRINT") {
    const value = parts[1];
    console.log(`Output: ${value}`);
  } else if (parts[0].toUpperCase() === "ASSIGN") {
    const variableName = parts[1];
    const value = parts[2];
    //In JavaScript, use 'let' or 'const' to declare variables
    eval(`let ${variableName} = ${value};`); // Use eval carefully!
    console.log(`Variable '${variableName}' assigned value ${value}`);
  } else if (parts[0].toUpperCase() === "FUNCTION") {
    const functionName = parts[1];
    const functionBody = parts.slice(2).join(" ");
    functions[functionName] = functionBody;
    console.log(`Function '${functionName}' defined.`);
  } else if (parts[0].toUpperCase() === "CALL") {
    const functionName = parts[1];
    if (functionName in functions) {
      try {
        eval(functions[functionName]); //Use eval carefully!
        console.log(`Function '${functionName}' executed.`);
      } catch (error) {
        console.error(`Error executing '${functionName}': ${error}`);
      }
    } else {
      console.log(`Function '${functionName}' not found.`);
    }
  } else {
    console.log("Instruction not recognized.");
  }
  return true; // Continue processing
}


//Example of how to integrate this into a webpage, using a prompt and displaying results
let keepGoing = true;
while (keepGoing) {
    const instruction = prompt("Enter instruction (ADD, PRINT, ASSIGN, FUNCTION, CALL, EXIT):");
    keepGoing = processInstruction(instruction);
}
