import React, { Component } from 'react';
import BootstrapTable from 'react-bootstrap-table-next';
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';
import { Button } from 'semantic-ui-react';
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
    }, {
      dataField: 'text',
      text: 'Text',
    }, {
      dataField: 'test',
      isDummyField: true,
      text: '',
      // eslint-disable-next-line arrow-body-style
      formatter: (cellContent, row) => {
        return (
          <Button color="red" icon="trash" onClick={() => this.handleOnClickDelete(row)} />
        );
      },
    }],
  }

  componentDidMount() {
    this.syncAnnouncements();
  }

  handleOnClickDelete = (row) => {
    console.log(row);
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
