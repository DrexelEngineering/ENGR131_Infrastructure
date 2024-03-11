document.addEventListener("DOMContentLoaded", function () {
  fetchSubmissions();
});

async function fetchSubmissions() {
  try {
    const response = await fetch("/get-submissions");
    const data = await response.json();
    populateTable(data);
  } catch (error) {
    console.error("Error fetching submissions:", error);
  }
}

function populateTable(submissions) {
  const tableBody = document
    .getElementById("submissionsTable")
    .getElementsByTagName("tbody")[0];
  tableBody.innerHTML = ""; // Clear existing table data

  submissions.forEach((submission) => {
    let row = `<tr>
            <td>${submission.submission_id}</td>
            <td>${submission.original_file_name}</td>
            <td>${submission.student_id}</td>
            <td>${submission.assignment_id}</td>
            <td>${submission.submitter_type}</td>
            <td>${submission.total_score}</td>
            <td>${submission.max_score}</td>
            <td>${submission.percentage_score}</td>
            <td>${submission.submission_time}</td>
            <td>${submission.start_time}</td>
            <td>${submission.end_time}</td>
            <td>${submission.flag}</td>
            <td>${submission.submission_mechanism}</td>
        </tr>`;
    tableBody.innerHTML += row;
  });
}

function filterSubmissions() {
  const filterValue = document.getElementById("filter").value;
  fetchSubmissions(); // In a real-world scenario, you would adjust this to filter on the server-side
  // For client-side filtering, adjust the populateTable function to filter based on `filterValue`
}
