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
      dataField: 'privilege_category.name',
      text: 'Privilege Category',
      align: 'center',
    }, {
      dataField: 'dummy',
      text: '',
      align: 'center',
      isDummyField: true,
      formatter: (col, row) => (
        <Button color="blue" onClick={() => this.openModal(row)}>Members</Button>
      ),
    }],
  }

  componentDidMount() {
    this.syncGroups();
  }

  syncGroups = () => {
    // eslint-disable-next-line react/prop-types
    const { selectedGroup } = this.props;

    this.setState({ isLoading: true });
    api.getMyGroups()
      .then((r) => {
        this.setState({
          groups: r.data,
          isLoading: false,
        });
        if (selectedGroup) {
          const group = r.data.find((g) => {
            // eslint-disable-next-line eqeqeq
            if (g.id == selectedGroup) {
              return true;
            }
            return false;
          });
          this.openModal(group);
        }
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
    return (
      <Modal open onClose={this.closeModal} size="tiny">
        <Modal.Header>
          {`Group: ${modalContent.name}`}
        </Modal.Header>
        <Modal.Content>
          <h3>Members</h3>
          <List divided>
            {modalContent.members.map(m => (
              <MemberRowItem
                key={m.id}
                member={m}
                // eslint-disable-next-line no-console
                deleteFunction={() => console.log()}
                isAdmin={false}
              />
            ))}
          </List>
        </Modal.Content>
      </Modal>
    );
  }

  render() {
    const {
      isLoading, groups, columns, showModal, modalContent,
    } = this.state;
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
