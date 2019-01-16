import React, { Component } from 'react';
import { withRouter } from 'react-router-dom';
import { Icon } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import './SideNav.scss';


class SideNav extends Component {
  renderNavItem = () => {
    // eslint-disable-next-line react/prop-types
    const { selectedMenu, navConfig, history } = this.props;

    const rows = [];
    // eslint-disable-next-line array-callback-return
    navConfig.map((config) => {
      let { text } = config;
      if (text === 'Calendar') {
        text = (
          <div>
            <Icon name="arrow left" />
            {text}
          </div>
        );
      }

      rows.push(
        <li
          className={selectedMenu === config.menu ? 'active' : ''}
          onClick={() => { history.push(config.path); }}
          key={config.menu}
          onKeyDown={() => {}}
        >
          {text}
        </li>,
      );
    });
    return (
      <ul>
        {rows}
      </ul>
    );
  }

  render() {
    return (
      <div className="sidenav">
        {this.renderNavItem()}
      </div>
    );
  }
}

SideNav.propTypes = {
  selectedMenu: PropTypes.string.isRequired,
  // eslint-disable-next-line react/forbid-prop-types
  navConfig: PropTypes.array,
};

SideNav.defaultProps = {
  navConfig: [
    { text: 'Calendar', menu: 'calendar', path: '/' },
    { text: 'Settings', menu: 'settings', path: '/admin/settings' },
    { text: 'Privileges', menu: 'privileges', path: '/admin/privileges' },
    { text: 'Rooms', menu: 'rooms', path: '/admin/rooms' },
    { text: 'Stats', menu: 'stats', path: '/admin/stats' },
    { text: 'Bookers', menu: 'bookers', path: '/admin/bookers' },
  ],
};

export default withRouter(SideNav);
