(function($) {

function createUrlFn(category) {
    return function(query) {
        return '/results/query.json' +  '?category=' +
               category + '&q=' + escape(query);
    }
}

$(function() {

    $('.ui-ls-autocomplete').livesearch({
        urlFn: createUrlFn('all'),
        search: function(event, ui) {
            $('<p>Search for ' + ui.query + '</p>')
                .prependTo($('.bc-content-frame'));
        },
        menu: function(event, ui) {
            var text = ui.text;
            var category = text;
            if (category === 'All Content') {
                category = 'all';
            }
            var urlFn = createUrlFn(category)
            $('.ui-ls-autocomplete').livesearch('option', 'urlFn', urlFn);
        },
        validationFn: $.bottlecap.livesearch.prototype.numCharsValidate,
        queryTransformFn: $.bottlecap.livesearch.prototype.globQueryTransform,
        errorFn: $.bottlecap.livesearch.prototype.displayError,
        renderCompletions: renderCompletions
    });

    // The magnifying glass button on the right
    $(".ui-ls-gobtn").button({
        text: false,
        icons: {primary: "ui-icon-search"}
    });

    // XXX should this be in the livesearch widget itself?
    // Dynamically set some positioning
    $('.ui-ls-autocomplete')
        .height($('.ui-ls-menu').height()+1)
        .focus();
    $('.ui-ls-autocomplete').position({
        of: $('.ui-ls-menu'),
        at: "right top",
        my: "left top"
    });
});

function renderCompletions(ul, items) {
    var self = this,
        currentCategory = "";
    $.each(items, function(index, item) {
        // Change autocomplete behavior which overrides the
        // searchterm
        item.data_value = item.value;
        item.value = self.term;
         if (item.category !== currentCategory) {
            var li = $('<li class="ui-autocomplete-category"></li>');
            li.append(
                $('<span class="ui-ls-category-text"></span>')
                    .text(item.category)
            );
            li.append(
                $('<span class="ui-ls-more"></span>')
                    .attr('href', '/search/more')
                    .text('more')
                    .click((function(category) {
                        return function() {
                            $('<p>More link clicked for '
                              + category + '</p>')
                                .prependTo($('.bc-content-frame'));
                            return false;
                        };
                    })(item.category))
            );
            ul.append(li);
            currentCategory = item.category;
        }
        renderItem(ul, item);
    });
    // Set a class on the first item, to remove a border on
    // the first row
    ul.find('li:first').addClass('ui-ls-autocomplete-first');
}

var renderDispatchTable = {
    "profile":   renderPersonEntry,
    "wikipage":  renderPageEntry,
    "blogentry": renderPostEntry,
    "file":      renderFileEntry
};

function renderPersonEntry(item) {
    var entry = $('<a class="ui-ls-profile"></a>');
    entry.append($('<img>')
                 .attr('src', '/bottlecap/sl/livesearch/' + item.icon));
    var userInfoDiv = $('<div class="user">')
        .append($('<div>').text(item.label))
        .append($('<div>').text(item.department));
    var contactDiv = $('<div class="contact">')
        .append($('<div>')                 //.text(item.email))
                .append($('<a>')
                        .attr('href', 'mailto:' + item.email)
                        .text(item.email)
                        .click(function() {
                            window.location = 'mailto:' + item.email;
                            return false;
                        })))
        .append($('<div>').text(item.extension));
    entry.append(userInfoDiv).append(contactDiv)
        .append($('<div style="clear: both">'));
    return entry;
}

function renderGenericEntry(item) {
    return $("<a></a>").text(item.label);
}

function renderPageEntry(item) {
    var entry = $('<a class="ui-ls-page">');
    entry
        .append($('<div>')
                .append($('<span>').text(item.label))
                .append($('<span class="discreet">').text(
                    ' - by ' + item.author + ' on ' + item.modified)))
        .append($('<div>').text(item.community));
    return entry;
}

function renderPostEntry(item) {
    var entry = $('<a class="ui-ls-post">');
    entry
        .append($('<div>')
                .append($('<span>').text(item.label))
                .append($('<span class="discreet">').text(
                    ' - by ' + item.author + ' on ' + item.created)))
        .append($('<div>').text(item.community));
    return entry;
}

function renderFileEntry(item) {
    var entry = $('<a class="ui-ls-file">');
    entry
        .append($('<img>')
                .attr('src', '/bottlecap/sl/livesearch/' + item.icon))
        .append($('<div>').text(item.label))
        .append($('<div class="discreet">').text(
            'by ' + item.author + ' on ' + item.modified));
    return entry;
}

function renderItem(ul, item) {
    var li = $('<li>');
    // Render different items in different ways
    // dispatch based on the type of the item
    var type     = item.type,
        renderFn = renderDispatchTable[type] || renderGenericEntry,
        entry    = renderFn(item);
    return $("<li></li>")
        .data("item.autocomplete", item)
        .append(entry)
        .appendTo(ul);
}


})(jQuery);
