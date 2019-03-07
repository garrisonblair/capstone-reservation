import React, { Component } from 'react';
import { isMobile } from 'react-device-detect';
import withTracker from '../HOC/withTracker';
import Calendar from '../Calendar';
import './Home.scss';


class Home extends Component {
  componentDidMount = () => {
    // eslint-disable-next-line react/prop-types
    const { history } = this.props;

    document.title = 'Home';

    if (isMobile) {
      history.push('/mobile_home');
    }
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
