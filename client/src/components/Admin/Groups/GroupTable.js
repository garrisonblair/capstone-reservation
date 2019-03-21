import React, { Component } from 'react';
import {
  Segment, Button, Modal, List,
} from 'semantic-ui-react';
import BootstrapTable from 'react-bootstrap-table-next';
import './GroupsTable.scss';
import api from '../../../utils/api';
import MemberRowItem from '../../Groups/MemberRowItem';

class GroupsTable extends Component {
  state = {
    showModal: false,
    isLoading: false,
    groups: [],
    columns: [{
      dataField: 'id',
      text: 'Id',
      align: 'center',
    }, {
      dataField: 'name',
      text: 'Name',
      align: 'center',
    }, {
      dataField: 'owner.username',
      text: 'Owner',
      align: 'center',
    }, {
      dataField: 'dummy',
      text: '',
      align: 'center',
      isDummyField: true,
      formatter: (col, row) => (
        <Button color="blue" onClick={() => this.openModal(row)}>Details</Button>
      ),
    }],
  }

  componentDidMount() {
    this.syncGroups();
  }

  syncGroups = () => {
    this.setState({ isLoading: true });
    api.getMyGroups()
      .then((r) => {
        this.setState({
          groups: r.data,
          isLoading: false,
        });
      });
  }

  openModal = (content) => {
    this.setState({
      showModal: true,
      modalContent: content,
    });
  }

  closeModal = () => {
    this.setState({ showModal: false });
  }

  renderModal = () => {
    const { modalContent } = this.state;
    console.log(modalContent);
    return (
      <Modal open onClose={this.closeModal} size="tiny">
        <Modal.Header>
          {`Group: ${modalContent.name}`}
        </Modal.Header>
        <Modal.Content>
          <List>
            {modalContent.members.map(m => (
              <MemberRowItem
                key={m.id}
                member={m}
                deleteFunction={() => console.log()}
                isAdmin
              />
            ))}
          </List>
          {/* <MemberRowItem /> */}
        </Modal.Content>
      </Modal>
    );
  }

  render() {
    const {
      isLoading, groups, columns, showModal, modalContent,
    } = this.state;
    console.log(groups);
    return (
      <div id="groups-table">
        <Segment loading={isLoading}>
          <BootstrapTable
            noDataIndication="There are no groups."
            keyField="id"
            data={groups}
            columns={columns}
          />
        </Segment>
        {showModal ? this.renderModal(modalContent) : null}
      </div>
    );
  }
}

export default GroupsTable;
