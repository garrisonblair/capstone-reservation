function generateMinuteOptions(minuteInterval) {
  const result = [];
  for (let i = 0; i < 60; i += minuteInterval) {
    result.push({
      text: `${i < 10 ? `0${i}` : i}`,
      value: `${i < 10 ? `0${i}` : i}`,
    });
  }
  return result;
}

const timeUtil = {
  generateMinuteOptions,
};

export default timeUtil;
