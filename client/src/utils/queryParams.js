

function parse(queryString) {
  const query = queryString.substring(1, queryString.length - 1).split('&');

  const queryParams = query.reduce((params, currentParam) => {
    const keyValuePair = currentParam.split('=');
    // eslint-disable-next-line prefer-const
    let [key, value] = keyValuePair;
    if (value === 'true') {
      value = true;
    } else if (keyValuePair[1] === 'false') {
      value = false;
    }
    // eslint-disable-next-line no-param-reassign
    params[key] = value;
    return params;
  }, {});

  return queryParams;
}

const queryParams = {
  parse,
};

export default queryParams;
