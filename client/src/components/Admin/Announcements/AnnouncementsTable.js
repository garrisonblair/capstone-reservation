import React, { Component } from 'react';
import BootstrapTable from 'react-bootstrap-table-next';
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';
import { Button } from 'semantic-ui-react';
import api from '../../../utils/api';
// import sweetAlert from 'sweetalert2';
// import api from '../../../utils/api';
// import './AnnouncementsTable.scss';

class AnnouncementsTable extends Component {
  state = {
    announcements: [],
    columns: [
      {
        dataField: 'id',
        text: 'myId',
      },
      {
        dataField: 'title',
        text: 'mysubject',
      },
      {
        dataField: 'content',
        text: 'Text',
      },
      {
        dataField: 'start_date',
        text: 'From',
      },
      {
        dataField: 'end_date',
        text: 'To',
      },
      {
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
    api.getAllAnnouncements()
      .then((r) => {
        console.log(r);
        if (r.status === 200) {
          this.setState({ announcements: r.data });
        }
      });
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
