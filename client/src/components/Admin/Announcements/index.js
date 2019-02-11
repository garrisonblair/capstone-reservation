import React, { Component } from 'react';
import AddAnnouncementForm from './AddAnnouncementForm';
// import { Table, Segment } from 'semantic-ui-react';
// import sweetAlert from 'sweetalert2';
// import api from '../../../utils/api';
import './Announcements.scss';
import AnnouncementsTable from './AnnouncementsTable';

class Announcements extends Component {
  announcementsTable = React.createRef();

  syncAnnouncements = () => {
    this.announcementsTable.current.syncAnnouncements();
  }

  render() {
    return (
      <div id="announcements">
        <h1>Announcements</h1>
        <AddAnnouncementForm syncFunction={this.syncAnnouncements} />
        <br />
        <br />
        <AnnouncementsTable ref={this.announcementsTable} />
      </div>
    );
  }
}

export default Announcements;
