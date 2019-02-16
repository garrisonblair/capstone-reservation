import React, { Component } from 'react';
import AddAnnouncementForm from './AddAnnouncementForm';
import AnnouncementsTable from './AnnouncementsTable';
import './Announcements.scss';


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
