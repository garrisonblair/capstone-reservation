import React, { Component } from 'react';
import BootstrapTable from 'react-bootstrap-table-next';
import cellEditFactory, { Type } from 'react-bootstrap-table2-editor';
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';
import { Button, Segment } from 'semantic-ui-react';
import sweetAlert from 'sweetalert2';
import api from '../../../utils/api';
import './AnnouncementsTable.scss';

class AnnouncementsTable extends Component {
  state = {
    isLoading: false,
    announcements: [],
    columns: [
      {
        dataField: 'title',
        text: 'Title',
        // eslint-disable-next-line arrow-body-style
        formatter: (cell) => {
          return (
            <strong>
              {cell}
            </strong>
          );
        },
      },
      {
        dataField: 'content',
        text: 'Text',
        editor: {
          type: Type.TEXTAREA,
        },
      },
      {
        dataField: 'start_date',
        text: 'From',
        align: 'center',
        editor: {
          type: Type.DATE,
        },
        // eslint-disable-next-line consistent-return
        validator: (newValue, row) => {
          if (new Date(newValue) > new Date(row.end_date)) {
            return { valid: false, message: 'Start date should not be after end date.' };
          }
        },
      },
      {
        dataField: 'end_date',
        text: 'To',
        align: 'center',
        editor: {
          type: Type.DATE,
        },
        // eslint-disable-next-line consistent-return
        validator: (newValue, row) => {
          if (new Date(newValue) < new Date(row.end_date)) {
            return { valid: false, message: 'End date should not be before start date.' };
          }
        },
      },
      {
        dataField: 'test',
        isDummyField: true,
        text: '',
        align: 'center',
        editable: false,
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
    sweetAlert.fire({
      text: `Are you sure you want to delete announcement with title '${row.title}'?`,
      type: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      confirmButtonText: 'Yes, delete it!',
    }).then((r) => {
      if (r.value) {
        api.deleteAnnouncement(row.id)
          .then((r2) => {
            if (r2.status === 204) {
              sweetAlert('Success', 'Deleted', 'success');
              this.syncAnnouncements();
            }
          });
      }
    });
  }

  syncAnnouncements = () => {
    this.setState({ isLoading: true });
    api.getAllAnnouncements()
      .then((r) => {
        if (r.status === 200) {
          this.setState({ announcements: r.data, isLoading: false });
        }
      });
  }

  render() {
    const { announcements, columns, isLoading } = this.state;
    return (
      <div id="announcement-table">
        <Segment loading={isLoading}>
          <BootstrapTable
            noDataIndication="There are no announcements."
            keyField="id"
            data={announcements}
            columns={columns}
            cellEdit={
              cellEditFactory({
                mode: 'dbclick',
                blurToSave: true,
                afterSaveCell: (oldValue, newValue, row) => api.updateAnnouncement(row),
              })}
            caption="Double click on cell to edit."
          />
        </Segment>
      </div>
    );
  }
}

export default AnnouncementsTable;
