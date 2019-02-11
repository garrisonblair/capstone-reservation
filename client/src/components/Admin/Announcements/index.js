import React, { Component } from 'react';
import AddAnnouncementForm from './AddAnnouncementForm';
// import { Table, Segment } from 'semantic-ui-react';
// import sweetAlert from 'sweetalert2';
// import api from '../../../utils/api';
import './Announcements.scss';

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
        <AddAnnouncementForm syncFunction={this.syncAnnouncements} />
      </div>
    );
  }
}

export default Announcements;
