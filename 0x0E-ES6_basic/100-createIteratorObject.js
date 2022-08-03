export default function createIteratorObject(report) {
  const employees = Object.values(report.allEmployees);
  const employeesList = [];
  for (const employee of employees) employeesList.push(...employee);
  return employeesList;
}
