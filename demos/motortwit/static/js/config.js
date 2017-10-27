/* global _ angular */
(function () {
    'use strict';
    var onSubmitError = function (error, form, progression, notification) {
        // mark fields based on errors from the response
        if (!('error_details' in error.data)) {
            return true;
        }
        _.mapObject(error.data.error_details, function (error_msg, field_name) {
            if (form[field_name]) {
                form[field_name].$valid = false;
            }
            return {};
        });
        // stop the progress bar
        progression.done();
        // add a notification
        notification.log('Some values are invalid, see details in the form',
            {addnCls: 'humane-flatty-error'});
        // cancel the default action (default error messages)
        return false;
    };


    var app = angular.module('aiohttp_admin', ['ng-admin']);
    app.config(['RestangularProvider', function (RestangularProvider) {
        var token = window.localStorage.getItem('aiohttp_admin_token');
        RestangularProvider.setDefaultHeaders({'Authorization': token});
    }]);

    app.config(['NgAdminConfigurationProvider', function (nga) {
        var admin = nga.application('aiohttp admin demo');

        admin.baseApiUrl('/admin/');

        admin.errorMessage(function (response) {
            var msg = '<p>Oops error occured with status code: ' + response.status + '</p>\n';

            if ('error_details' in response.data) {
                msg += '<code>';
                msg += JSON.stringify(response.data.error_details, null, 2);
                msg += '</code>';
            }
            return msg;
        });

        var user = nga.entity('user').identifier(nga.field('_id'));
        var message = nga.entity('message').identifier(nga.field('_id'));
        var follower = nga.entity('follower').identifier(nga.field('_id'));

        admin
            .addEntity(user)
            .addEntity(message)
            .addEntity(follower);

        user.listView()
            .title('All users')
            .description('List of users with infinite pagination')
            .infinitePagination(true)
            .perPage(50)
            .fields([
                nga.field('_id').isDetailLink(true),
                nga.field('username'),
                nga.field('email', 'email'),
            ])
            .filters([
                nga.field('username')
                    .attributes({'placeholder': 'Filter by username'}),
            ])
            .sortField('_id')
            .listActions(['show', 'edit', 'delete']);

        user.creationView()
            .fields([
                nga.field('username'),
                nga.field('email', 'email'),
                nga.field('pw_hash'),
            ]);
        user.creationView()
            .onSubmitError(['error', 'form', 'progression', 'notification', onSubmitError]);

        user.editionView()
            .title('Edit user')
            .actions(['list', 'show', 'delete'])
            .fields([
                nga.field('_id')
                    .editable(false),
                user.creationView().fields(),
                nga.field('message', 'referenced_list')
                    .targetEntity(nga.entity('message').identifier(nga.field('_id')))
                    .targetReferenceField('author_id')
                    .targetFields([
                        nga.field('_id').isDetailLink(true),
                        nga.field('text'),
                        nga.field('pub_date')
                    ])
                    .sortField('_id')
                    .sortDir('DESC')
                    .listActions(['edit']),
            ]);

        user.editionView()
            .onSubmitError(['error', 'form', 'progression', 'notification', onSubmitError]);

        user.showView()
            .fields([
                nga.field('_id'),
                nga.field('username'),
                nga.field('email', 'email'),
                nga.field('pw_hash'),
                nga.field('message', 'referenced_list')
                    .targetEntity(nga.entity('message'))
                    .targetReferenceField('author_id')
                    .targetFields([
                        nga.field('_id').isDetailLink(true),
                        nga.field('text').label('Message text'),
                        nga.field('pub_date').label('Publish date')
                    ])
                    .sortField('_id')
                    .sortDir('DESC')
                    .listActions(['edit']),
            ]);

        message.listView()
            .title('Messages')
            .perPage(10)
            .fields([
                nga.field('_id').isDetailLink(true),
                nga.field('author_id'),
                nga.field('username'),
                nga.field('text'),
                nga.field('pub_date'),
            ])
            .sortField('_id')
            .listActions(['edit', 'delete']);

        message.creationView()
            .fields([
                nga.field('author_id', 'reference')
                    .label('User')
                    .targetEntity(user)
                    .targetField(nga.field('username'))
                    .sortField('_id')
                    .sortDir('ASC')
                    .validation({required: true})
                    .remoteComplete(true, {
                        refreshDelay: 200,
                        searchQuery: function (search) {
                            return {q: search};
                        }
                    }),
                nga.field('username'),
                nga.field('text'),
                nga.field('pub_date'),
            ]);

        message.creationView().onSubmitError(['error', 'form', 'progression', 'notification', onSubmitError]);

        message.editionView()
            .fields(
                nga.field('_id')
                    .editable(false)
                    .label('_id'),
                message.creationView().fields()
            );
        message.editionView()
            .onSubmitError(['error', 'form', 'progression', 'notification', onSubmitError]);

        message.deletionView()
            .title('Deletion confirmation');

        follower.listView()
            .title('All follower')
            .fields([
                nga.field('_id').isDetailLink(true),
                nga.field('who_id'),
                nga.field('whom_id', 'reference_many')
                    .targetEntity(user)
                    .targetField(nga.field('username'))
            ])
            .sortField('_id')
            .listActions(['show', 'edit', 'delete']);

        follower.editionView()
            .fields([
                nga.field('_id').isDetailLink(true),
                nga.field('who_id', 'reference')
                    .label('User')
                    .targetEntity(user)
                    .targetField(nga.field('username'))
                    .sortField('_id')
                    .sortDir('ASC')
                    .validation({required: true})
                    .remoteComplete(true, {
                        refreshDelay: 200,
                        searchQuery: function (search) {
                            return {q: search};
                        }
                    }),
                nga.field('whom_id', 'reference_many')
                    .targetEntity(user)
                    .targetField(nga.field('username'))
            ]);

        follower.deletionView()
            .title('Deletion confirmation');

        nga.configure(admin);
    }]);

}());
