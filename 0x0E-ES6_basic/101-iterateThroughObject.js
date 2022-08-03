export default function iterateThroughObject(reportWithIterator) {
  let result = '';
  for (let index = 0; index < reportWithIterator.length; index += 1) {
    const len = reportWithIterator.length - 1;
    if (index === len) {
      result += `${reportWithIterator[index]}`;
    } else {
      result += `${reportWithIterator[index]} | `;
    }
  }
  return result;
}
