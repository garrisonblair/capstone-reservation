import React, { Component } from 'react';
import withTracker from '../HOC/withTracker';
import Calendar from '../Calendar';
import './Home.scss';


class Home extends Component {
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
