/* eslint-disable react/prefer-stateless-function */
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  Header,
  Icon,
  Segment,
} from 'semantic-ui-react';

class EmptySegment extends Component {
  render() {
    const { message, loading } = this.props;
    return (
      <Segment placeholder textAlign="center" loading={loading}>
        <Header icon>
          <Icon name="ban" />
          {message}
        </Header>
      </Segment>
    );
  }
}

EmptySegment.propTypes = {
  message: PropTypes.string.isRequired,
  loading: PropTypes.bool,
};

EmptySegment.defaultProps = {
  loading: false,
};

export default EmptySegment;
