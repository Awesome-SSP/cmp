const { exec } = require('child_process');

// Run the Python script
exec('python 1.py', (error, stdout, stderr) => {
  if (error) {
    console.error(`❌ Error: ${error.message}`);
    return;
  }
  if (stderr) {
    console.error(`⚠️ Stderr: ${stderr}`);
    return;
  }
  console.log(`✅ Output:\n${stdout}`);
});
