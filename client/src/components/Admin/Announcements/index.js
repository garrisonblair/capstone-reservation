import React, { Component } from 'react';
// import { Table, Segment } from 'semantic-ui-react';
// import sweetAlert from 'sweetalert2';
// import api from '../../../utils/api';

class Announcements extends Component {
  state = {
    // announcements: [],
  }

  componentDidMount() {
    this.syncAnnouncements();
  }

  syncAnnouncements = () => {

  }

  render() {
    return (
      <div id="announcements">
        <h1>Announcements</h1>
      </div>
    );
  }
}

export default Announcements;
