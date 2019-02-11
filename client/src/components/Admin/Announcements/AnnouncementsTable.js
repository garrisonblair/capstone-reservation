import React, { Component } from 'react';
import BootstrapTable from 'react-bootstrap-table-next';
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';
// import { Table, Segment } from 'semantic-ui-react';
// import sweetAlert from 'sweetalert2';
// import api from '../../../utils/api';
// import './AnnouncementsTable.scss';

class AnnouncementsTable extends Component {
  state = {
    announcements: [],
    columns: [{
      dataField: 'id',
      text: 'myId',
    }, {
      dataField: 'subject',
      text: 'mysubject',
    }],
  }

  componentDidMount() {
    this.syncAnnouncements();
  }

  syncAnnouncements = () => {
    const { announcements } = this.state;
    announcements.push({ id: announcements.length, subject: 'as', text: 'dd' });
    this.setState({ announcements });
  }

  render() {
    const { announcements, columns } = this.state;
    return (
      <div id="announcement-table">
        <BootstrapTable keyField="id" data={announcements} columns={columns} />
      </div>
    );
  }
}

export default AnnouncementsTable;
