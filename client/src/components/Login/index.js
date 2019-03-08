/* eslint-disable react/prop-types */
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withRouter } from 'react-router-dom';
import {
  Modal,
} from 'semantic-ui-react';
import './Login.scss';
import LoginComponent from './login';

class Login extends Component {
  state = {
    show: false,
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.show) {
      this.setState({
        show: nextProps.show,
      });
    }
  }

  closeModal = () => {
    const { onClose } = this.props;
    onClose();
    this.setState({
      show: false,
    });
  }

  render() {
    const { show } = this.state;
    return (
      <Modal open={show} onClose={this.closeModal} className="login__container" centered={false}>
        <Modal.Header>
          <h1 className="login__container__header__title"> Login </h1>
        </Modal.Header>
        <Modal.Content>
          <LoginComponent onSuccess={this.closeModal} />
        </Modal.Content>
      </Modal>
    );
  }
}

Login.propTypes = {
  show: PropTypes.bool.isRequired,
  onClose: PropTypes.func,
};

Login.defaultProps = {
  onClose: () => {
    const { onClose } = this.props;
    onClose();
    this.setState({
      show: false,
    });
  },
};

export default withRouter(Login);
