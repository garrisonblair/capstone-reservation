import React, { Component } from 'react';
import { isMobile } from 'react-device-detect';
import withTracker from '../HOC/withTracker';
import Calendar from '../Calendar';
import './Home.scss';


class Home extends Component {
  constructor(props) {
    super(props);
    // eslint-disable-next-line react/prop-types
    const { history, location } = props;

    const queryString = location.search;
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

    if (isMobile && !queryParams.forceDesktop) {
      history.push('/mobile_home');
    }
  }

  componentDidMount = () => {
    document.title = 'Home';
  }

  render() {
    return (
      <div>
        <main>
          <Calendar />
        </main>
      </div>
    );
  }
}

export default withTracker(Home);
