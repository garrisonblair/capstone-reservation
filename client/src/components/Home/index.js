import React, { Component } from 'react';
import { isMobileOnly } from 'react-device-detect';
import withTracker from '../HOC/withTracker';
import Calendar from '../Calendar';
import queryParams from '../../utils/queryParams';
import './Home.scss';


class Home extends Component {
  constructor(props) {
    super(props);
    // eslint-disable-next-line react/prop-types
    const { history, location } = props;

    const query = queryParams.parse(location.search);

    if (isMobileOnly && !query.forceDesktop) {
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
